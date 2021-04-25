import argparse
import socket
import cv2
import utils
from datetime import datetime

def startServer(host,port):

    # Creating a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_host_name = socket.gethostname()
    server_host_ip = socket.gethostbyname(server_host_name)
    socket_address = (server_host_ip,port)

    # Binding a socket
    sock.bind(('0.0.0.0', port))

    # Listening to socket
    sock.listen()
    print('Server Listening at: ',socket_address)

    # Accepting a socket connnection
    while True:
        conn, addr = sock.accept()
        print('Accepted a Client Connection from: ',addr)
        print('  Socket Name: ', conn.getsockname())
        print('  Socket Peer: ', conn.getpeername())
        if conn:
            # Creating a Video Capture Object for opencv
            video_capture_object  = cv2.VideoCapture(0)
            if not video_capture_object.isOpened():
                conn.close()
                raise IOError('Cannot open webcam')
            starttime = datetime.now()
            print('  Started Video Streaming at :', starttime.strftime('%I:%M:%S'), starttime.strftime('%d-%m-%Y'))

            frame_count = 0


            while(True):
                img, frame = video_capture_object.read()
                # Handles the mirroring of the current frame
                frame = cv2.flip(frame,1)
                frame = cv2.resize(frame, None, fx=  0.5, fy = 0.5, interpolation = cv2.INTER_AREA)
                # Sending even half frame across the subflow
                conn.sendall(utils.encodeNumPyArray(frame, True))
                # Sending odd half frame across the subflow
                conn.sendall(utils.encodeNumPyArray(frame, False))
                frame_count += 1
                # Limiting the number of frames transmitted to 200
                if(frame_count==200):
                    break

            # When everything is done, release the capture
            video_capture_object.release()
            cv2.destroyAllWindows()
        endtime = datetime.now()
        print('  Ended video streaming at: ', endtime.strftime('%I:%M:%S'), endtime.strftime('%d-%m-%Y'))
        print('  Frames Sent to client: ', frame_count)
        conn.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send and Receive over Multipath TCP ( MPTCP )')
    parser.add_argument('host', help='Interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=8080,
                        help='TCP port (default 8080)')
    args = parser.parse_args()
    startServer(args.host, args.p)