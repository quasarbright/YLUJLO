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
        if(object.ReferenceEquals(this, boid))
        {
            return false;
        }
        Vector3 pos = boid.transform.position;
        Vector3 disp = pos - transform.position;
        Vector3 vel = rb.velocity;
        float dot = Vector3.Dot(vel, disp);
        return dot >= 0f;
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
