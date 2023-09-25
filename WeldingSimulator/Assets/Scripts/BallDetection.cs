using System;
using System.Net.Sockets;
using System.Text;
using UnityEngine;

public class BallDetection : MonoBehaviour
{
    public string serverAddress = "127.0.0.1";
    public int serverPort = 8080;

    private TcpClient client;
    private NetworkStream stream;
    private byte[] receiveBuffer = new byte[1024];

    private void Start()
    {
        ConnectToServer();
    }

    private void ConnectToServer()
    {
        try
        {
            client = new TcpClient(serverAddress, serverPort);
            stream = client.GetStream();
            Debug.Log("Connected to server.");

            // Receive data from the server
            int bytesRead = stream.Read(receiveBuffer, 0, receiveBuffer.Length);
            string receivedData = Encoding.UTF8.GetString(receiveBuffer, 0, bytesRead);
            Debug.Log("Received from server: " + receivedData);
        }
        catch (Exception e)
        {
            Debug.LogError("Error connecting to server: " + e.Message);
        }
    }

    private void OnDestroy()
    {
        if (client != null)
        {
            client.Close();
        }
    }
}