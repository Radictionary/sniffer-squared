package packet

import (
	// "fmt"
	"fmt"
	"io/ioutil"
	"log"
	"net"
	"os"
	"strings"
	"sync"
	"time"

	// "github.com/Radictionary/sniffer-squared/models"
	"github.com/google/gopacket"
	"github.com/google/gopacket/layers"
	"github.com/google/gopacket/pcap"
	"github.com/google/gopacket/pcapgo"
)

// DetectProtocol detects the protocol, source and destination address and returns what it is.
func DetectProtocol(packet gopacket.Packet) (string, string, string) {
	var protocol, sourceAddress, destAddress string

	network := packet.NetworkLayer()
	if network != nil {
		switch network.LayerType() {
		case layers.LayerTypeIPv4:
			protocol = "IPv4"
			ipv4, _ := network.(*layers.IPv4)
			sourceAddress = ipv4.SrcIP.String()
			destAddress = ipv4.DstIP.String()

			transport := packet.TransportLayer()
			if transport != nil && transport.LayerType() == layers.LayerTypeUDP {
				udp, _ := transport.(*layers.UDP)
				dnsLayer := packet.Layer(layers.LayerTypeDNS)
				if dnsLayer != nil {
					protocol = "DNS"
				} else if udp.DstPort == 53 || udp.SrcPort == 53 {
					protocol = "DNS"
				} else if udp.DstPort == 51820 || udp.SrcPort == 51820 {
					//BROKEN
					if payload := packet.ApplicationLayer(); payload != nil {
						payloadData := payload.Payload()
						if len(payloadData) >= 4 {
							protocol = "WIREGUARD"
						}
					}
				} else {
					protocol = "UDP"
				}
			}
		case layers.LayerTypeIPv6:
			protocol = "IPv6"
			ipv6, _ := network.(*layers.IPv6)
			sourceAddress = ipv6.SrcIP.String()
			destAddress = ipv6.DstIP.String()

			transport := packet.TransportLayer()
			if transport != nil && transport.LayerType() == layers.LayerTypeUDP {
				udp, _ := transport.(*layers.UDP)
				dnsLayer := packet.Layer(layers.LayerTypeDNS)
				if dnsLayer != nil {
					protocol = "DNS"
				} else if udp.DstPort == 53 || udp.SrcPort == 53 {
					protocol = "DNS"
				} else {
					protocol = "UDP"
				}
			}
		}
	}
	if arpLayer := packet.Layer(layers.LayerTypeARP); arpLayer != nil {
		protocol = "ARP"
		arpPacket := arpLayer.(*layers.ARP)
		sourceAddress = net.IP(arpPacket.SourceProtAddress).String()
		destAddress = net.IP(arpPacket.DstProtAddress).String()
	}

	if protocol == "" {
		protocol = "N/A"
	}

	return protocol, sourceAddress, destAddress
}

func DetectPackets() {
	iface := "en0"
	fileSave := "test.pcap"
	snaplen := int32(1600)
	promisc := false
	timeout := pcap.BlockForever

	// Open output pcap file
	pcapFile, err := os.Create(fileSave)
	if err != nil {
		log.Fatal("Error creating pcap file:", err)
	}
	defer pcapFile.Close()

	// Initialize pcap writer
	pcapWriter := pcapgo.NewWriter(pcapFile)
	if err := pcapWriter.WriteFileHeader(uint32(snaplen), layers.LinkTypeEthernet); err != nil {
		log.Fatal("Error writing file header:", err)
	}

	// Open the device for capturing
	handle, err := pcap.OpenLive(iface, snaplen, promisc, timeout)
	if err != nil {
		log.Fatal("Error opening device:", err)
	}
	defer handle.Close()

	packetSource := gopacket.NewPacketSource(handle, handle.LinkType())
	packetSource.NoCopy = true

	controlChan := make(chan bool)
	var wg sync.WaitGroup

	wg.Add(1)
	capturing := false
	go func() {
		defer wg.Done()
		for {
			select {
			case packet, ok := <-packetSource.Packets():
				if !ok || !capturing {
					continue
				}
				// Write the packet to the pcap file
				if err := pcapWriter.WritePacket(packet.Metadata().CaptureInfo, packet.Data()); err != nil {
					log.Println("Failed to write packet:", err)
				}
			case start := <-controlChan:
				if start {
					log.Println("Starting packet capture")
					capturing = true
				} else {
					log.Println("Stopping packet capture")
					capturing = false
				}
			}
		}
	}()

	// Example control logic
	go func() {
		for {
			filePath := "run.txt"

			// Read the content of the file
			content, err := ioutil.ReadFile(filePath)
			if err != nil {
				log.Fatalf("Failed to read file: %v", err)
			}

			fileContent := strings.TrimSpace(string(content))
			toRun := fileContent == "true"
			fmt.Println("it is:", toRun)
			// Start capturing
			if toRun && !capturing {controlChan <- true}

			// Stop capturing
			if !toRun && capturing{controlChan <- false}
			time.Sleep(5 * time.Second) // Pause for 5 seconds
		}
	}()

	wg.Wait()
}
