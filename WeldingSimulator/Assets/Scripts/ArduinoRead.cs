using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.IO.Ports;

public class ArduinoRead : MonoBehaviour
{
    public string portName = "COM3";  // Change this to the correct port name
    public int baudRate = 9600;

    private SerialPort serialPort;

    void Start()
    {
        serialPort = new SerialPort(portName, baudRate);
        serialPort.Open();
    }

    void Update()
    {
        if (serialPort.IsOpen)
        {
            string[] data = serialPort.ReadLine().Split(',');
            if (data.Length == 7)
            {
                if (data[0] == "A")
                {
                    // Parse accelerometer data
                    float accelX = float.Parse(data[1]);
                    float accelY = float.Parse(data[2]);
                    float accelZ = float.Parse(data[3]);

                    // Use accelerometer data in Unity (e.g., for movement)
                    // For example:
                    // Vector3 acceleration = new Vector3(accelX, accelY, accelZ);
                    // transform.Translate(acceleration * Time.deltaTime);
                }
                else if (data[0] == "G")
                {
                    // Parse gyroscope data
                    float gyroX = float.Parse(data[1]);
                    float gyroY = float.Parse(data[2]);
                    float gyroZ = float.Parse(data[3]);

                    // Use gyroscope data in Unity (e.g., for rotation)
                    // For example:
                    // transform.Rotate(gyroX, gyroY, gyroZ);
                }
            }
        }
    }

    void OnApplicationQuit()
    {
        if (serialPort != null && serialPort.IsOpen)
        {
            serialPort.Close();
        }
    }
}