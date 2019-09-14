using System.Collections;
using System.Collections.Generic;
using UnityEngine;
[RequireComponent(typeof(Rigidbody))]
public class FieldOfView : MonoBehaviour
{
    public GameObject population;
    public float radius = 10f;
    Rigidbody rb;
    GameObject[] boids;

    // Start is called before the first frame update
    void Start()
    {
        rb = GetComponent<Rigidbody>();
        PopulationBehavior popBehavior = population.GetComponent<PopulationBehavior>();
        boids = popBehavior.boids;
    }

    bool IsVisible(GameObject boid)
    {
        Vector3 pos = boid.transform.position;
        Vector3 disp = 
        Vector3 vel = rb.velocity;
        float dot = Vector3.Dot(vel, )
    }

    public List<GameObject> GetVisibleBoids()
    {
        List<GameObject> ans = new List<GameObject>();
        foreach (GameObject boid in boids)
        {
            
        }
        return ans;
    }
}
