package main

import (
	"github.com/Radictionary/sniffer-squared/packet"
)

const portNumber = ":8001"

func main() {
	packet.DetectPackets()
}
