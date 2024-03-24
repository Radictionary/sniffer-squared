package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/Radictionary/sniffer-squared/packet"
	"github.com/Radictionary/sniffer-squared/ws"
	"github.com/go-chi/chi"
	"github.com/go-chi/chi/middleware"
	"github.com/gorilla/websocket"
)

const portNumber string = ":3957"

var Clients = *ws.InitializeClients()

func packetsHandler(w http.ResponseWriter, r *http.Request) {
	var upgrader = websocket.Upgrader{
		CheckOrigin: websocket.IsWebSocketUpgrade,
	}
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Fatalln("Could not upgrade connection to websocket")
	}
	client := Clients.CreateClient("default", conn)
	client.InitializeClient()
	go func() {
		packet.DetectPackets(client.SendChan)
	}()
}

func routes() http.Handler {
	chi := chi.NewRouter() //hooray

	chi.Use(middleware.CleanPath)

	chi.Get("/packets", packetsHandler) //packet stream

	return chi
}

func main() {
	go packet.DetectPackets("")
	fmt.Printf("Staring application on http://localhost%v\n", portNumber)
	srv := &http.Server{
		Addr:    portNumber,
		Handler: routes(),
	}

	err := srv.ListenAndServe()
	if err != nil {
		log.Fatalf("Port %v not open. Exiting", portNumber)
	}
}
