package packet

import (
	// "fmt"
	"fmt"
	"log"
	"os"
	"strings"
	"sync"
	"time"

 	"github.com/google/gopacket"
	"github.com/google/gopacket/layers"
	"github.com/google/gopacket/pcap"
	"github.com/google/gopacket/pcapgo"
)

func DetectPackets() {
	iface := "en0"
	fileSave := "packets.pcap"
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
			content, err := os.ReadFile(filePath)
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
