package main

import webview "github.com/webview/webview_go"

func main() {
	debug := true
	w := webview.New(debug)
	defer w.Destroy()
	w.SetTitle("Minha App")
	w.SetSize(800, 600, 0)
	w.Navigate("https://www.example.com")
	w.Run()
}