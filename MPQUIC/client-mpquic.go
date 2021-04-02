package main

import (
	"crypto/tls"
	"fmt"
	"time"
	"encoding/binary"

	utils "./utils"
	config "./config"
	quic "github.com/lucas-clemente/quic-go"
	"gocv.io/x/gocv"
)

const addr = "10.0.2.2:"+config.PORT
var pl = fmt.Println

func main() {

	quicConfig := &quic.Config{
		CreatePaths: true,
	}

	pl("Trying to connect to: ", addr)
	sess, err := quic.DialAddr(addr, &tls.Config{InsecureSkipVerify: true}, quicConfig)
	utils.HandleError(err)

	stream, err := sess.OpenStream()
	utils.HandleError(err)

	pl("Connected to server\n")
	pl("Starting Video streaming\n")
	defer stream.Close()

	webcam, _ := gocv.VideoCaptureDevice(0)
	img := gocv.NewMat()
	start := time.Now()
	webcam.Read(&img)

    var dimens = make([]byte, 4)
	var bs = make([]byte, 2)
	binary.LittleEndian.PutUint16(bs, uint16(img.Rows()))
	copy(dimens[0:],bs)
	binary.LittleEndian.PutUint16(bs, uint16(img.Cols()))
	copy(dimens[2:],bs)
	stream.Write(dimens)

	var count = 1
	for ;count<=config.MAX_FRAMES;count++{
		webcam.Read(&img)
		var b = img.ToBytes()
		for ind:=0;ind<len(b);{
			var end = ind+config.BUFFER_SIZE
			if end>len(b){
				end = len(b)
			}
			stream.Write(b[ind:end])
			ind = end
		}

	}
	stream.Write([]byte{0,0,0,0})
	webcam.Close()

	elapsed := time.Since(start)
	pl("\nEnded video streaming at: ", elapsed, "Frames Received from server: ", count)

	stream.Close()
	stream.Close()
}
