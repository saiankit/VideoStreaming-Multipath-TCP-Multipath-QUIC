## Install Packages

``` pip install requirements.txt ```

## Start the mininet CLI

Using instructions from [README.md](../README.md) start the mininet CLI with the provided configuration

## Running the Application

In the mininet CLI, run <br>
``` xterm client server ```

This should bring up terminals for both the client and server mininet nodes

In the terminal for server, run <br>
``` python3 MPTCP/server-mptcp.py localhost -p <port> ```

In the terminal for client, run <br>
``` python3 MPTCP/client-mptcp.py 10.0.2.2 -p <port> ```

You should now see an output window with the video being streamed