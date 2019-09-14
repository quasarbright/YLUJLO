using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PopulationBehavior : MonoBehaviour
{
    public GameObject boidPrefab;
    public int popSize = 100;
    public GameObject boundingCube;
    
    [HideInInspector]
    public GameObject[] boids;
    // Start is called before the first frame update
    void Start()
    {
        boids = new GameObject[popSize];
        for (int i = 0; i < popSize; i++)
        {
            Vector3 pos = SpawnPoint();
            GameObject boidObj = Instantiate(boidPrefab, pos, transform.rotation);
        }
    }

    Vector3 SpawnPoint()
    {
        float xmin, xmax, ymin, ymax, zmin, zmax;
        Vector3 pos = boundingCube.transform.position;
        float length = boundingCube.transform.lossyScale.x;
        float width = boundingCube.transform.lossyScale.z;
        float height = boundingCube.transform.lossyScale.y;
        xmin = pos.x - length / 2f;
        xmax = pos.x - length / 2f;
        zmin = pos.z - width / 2f;
        zmax = pos.z - width / 2f;
        ymin = pos.y - height / 2f;
        ymax = pos.y - height / 2f;

        return new Vector3(Random.Range(xmin, xmax), Random.Range(ymin, ymax), Random.Range(zmin, zmax));
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
