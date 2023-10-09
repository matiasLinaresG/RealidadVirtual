using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;
using System.Threading;

public class BallDetection : MonoBehaviour
{
    Thread thread;
    public int connectionPort = 8080;
    TcpListener server;
    TcpClient client;
    bool running;
    public GameObject MainCamera;
    private float xRot, yRot, zRot;
    // cameraPosition is the data obtained from the real camera (x, y, distance). has to be transformed into xyz from the game camera
    Vector3 camPosition = Vector3.zero;
    // relPosition is the data being received in this example
    Vector3 relPosition = Vector3.zero;
    // absPosition is the world position for the tool object
    Vector3 absPosition = Vector3.zero;



    void Start()
    {
        // Receive on a separate thread so Unity doesn't freeze waiting for data
        ThreadStart ts = new ThreadStart(GetData);
        thread = new Thread(ts);
        thread.Start();
    }

    void GetData()
    {
        // Create the server
        server = new TcpListener(IPAddress.Any, connectionPort);
        server.Start();

        // Create a client to get the data stream
        client = server.AcceptTcpClient();

        // Start listening
        running = true;
        while (running)
        {
            Connection();
        }
        server.Stop();
    }

    void Connection()
    {
        // Read data from the network stream
        NetworkStream nwStream = client.GetStream();
        byte[] buffer = new byte[client.ReceiveBufferSize];
        int bytesRead = nwStream.Read(buffer, 0, client.ReceiveBufferSize);

        // Decode the bytes into a string
        string dataReceived = Encoding.UTF8.GetString(buffer, 0, bytesRead);
        
        // Make sure we're not getting an empty string
        //dataReceived.Trim();
        if (dataReceived != null && dataReceived != "")
        {
            // Convert the received string of data to the format we are using
            camPosition = ParseData(dataReceived);
            nwStream.Write(buffer, 0, bytesRead);
        }
    }

    // Use-case specific function, need to re-write this to interpret whatever data is being sent
    public static Vector3 ParseData(string dataString)
    {
        // Log data
        Debug.Log(dataString);
        // Remove the parentheses
        if (dataString.StartsWith("(") && dataString.EndsWith(")"))
        {
            dataString = dataString.Substring(1, dataString.Length - 2);
        }

        // Split the elements into an array
        string[] stringArray = dataString.Split(',');

        // Store as a Vector3
        Vector3 result = new Vector3(
            float.Parse(stringArray[0]),
            float.Parse(stringArray[1]),
            float.Parse(stringArray[2]));
        return result;
    }

    void Update()
    {
        // Set this object's position in the scene according to the position received, relative to the main camera

        // Get camera euler angles
        xRot = MainCamera.transform.eulerAngles[0];
        yRot = MainCamera.transform.eulerAngles[1];
        zRot = MainCamera.transform.eulerAngles[2];

        

        transform.position = position;
    }
}