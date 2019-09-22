using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GridBehavior : MonoBehaviour
{
    public int length = 10;
    public int height = 10;

    private GameObject[,] objects;
    // Start is called before the first frame update
    void Start()
    {
        objects = new GameObject[height, length];
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
