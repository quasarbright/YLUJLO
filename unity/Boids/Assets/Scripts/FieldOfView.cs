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
        Vector3 disp = boid.transform.position - transform.position;
        return disp.sqrMagnitude < radius * radius;        
    }

    public List<GameObject> GetVisibleBoids()
    {
        PopulationBehavior popBehavior = population.GetComponent<PopulationBehavior>();
        boids = popBehavior.boids;
        List<GameObject> ans = new List<GameObject>();
        foreach (GameObject boid in boids)
        {
            if(IsVisible(boid))
            {
                ans.Add(boid);
            }
        }
        return ans;
    }
}
