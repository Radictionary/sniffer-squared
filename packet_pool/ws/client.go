package ws

import (
	"encoding/json"
	"fmt"

	"github.com/gorilla/websocket"
)

type Clients struct {
	Clients []Client
}

type Client struct {
	Name string
	SendChan chan ClientMessage
	ReceiveChan chan ClientMessage
	StopChan chan struct{}
	Conn *websocket.Conn
	Listening bool
	PacketNumber *int32
}

type ClientMessage struct {
	Label string
	Message any
}

func InitializeClients() *Clients {
	return &Clients{
		// Clients: make(map[string]Client),
	}
}

func (c *Clients) CreateClient(name string, conn *websocket.Conn) *Client {
	var client = &Client{
		Name: name,
		SendChan: make(chan ClientMessage),
		ReceiveChan: make(chan ClientMessage),
		StopChan: make(chan struct{}),
		Conn: conn,
		PacketNumber: new(int32),
	}

	c.Clients = append(c.Clients, *client)
	return client
}
func (c *Client)InitializeClient() {
	go func () {
		for {
			_, message, err := c.Conn.ReadMessage()
			if err != nil {
				fmt.Println("error is:", err)
				return
			}

			var clientMessage ClientMessage
			json.Unmarshal(message, &clientMessage)

			c.ReceiveChan <- clientMessage
		}
	}()
	go func () {
		for message := range c.SendChan{
			c.Conn.WriteJSON(message)
		}
	}()
}


//Make sure to do some authentication before sending packets
//Sends JSON(Javascript Object Notation) to the frontend with the ClientMessage type
func (c *Client) SendJSON(label string, v any) {
	jsonData, _ := json.Marshal(v)
	c.SendChan <- ClientMessage{
		Label:   label,
		Message: string(jsonData),
	}
}

//Sends a string message to the frontend with the ClientMessage type
func (c *Client) SendMessage(label string, s string) {
	c.SendChan <- ClientMessage{
		Label:   label,
		Message: s,
	}
}