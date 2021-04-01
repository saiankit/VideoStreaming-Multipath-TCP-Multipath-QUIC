## Install Golang

- [golang](https://golang.org/) (v1.9.2 recommended)

## Install packages 

- [quic-go](https://github.com/lucas-clemente/quic-go)
- [mpquic](https://github.com/qdeconinck/mp-quic)
- [GoCV](https://gocv.io/)

##### Installation instruction for quic-go and mpquic are available [here](https://multipath-quic.org/2017/12/09/artifacts-available.html)

## Building the application

```
cd MPQUIC
go build client-mpquic.go
go build server-mpquic-go
```

## Running the application

In the mininet CLI, run <br>
``` xterm client server ```

This should bring up terminals for both the client and server mininet nodes

In the terminal for server, run <br>
``` MPQUIC/server-mpquic ```

In the terminal for client, run <br>
``` MPQUIC/client-mpquic ```

You should now see an output window with the video being streamed