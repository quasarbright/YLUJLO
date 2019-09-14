using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(FieldOfView))]
public class Alignment : MonoBehaviour
{
    public float strength = 10f;
    Rigidbody rb;
    FieldOfView fieldOfView;
    
    // Start is called before the first frame update
    void Start()
    {
        rb = GetComponent<Rigidbody>();
        fieldOfView = GetComponent<FieldOfView>();
    }

    Vector3 CalcForce()
    {
        List<GameObject> boidObjs = fieldOfView.GetVisibleBoids();
        Vector3 resultant = new Vector3();
        foreach (GameObject boid in boidObjs)
        {
            resultant += boid.GetComponent<Rigidbody>().velocity;
        }
        return (resultant /= boidObjs.Count) - rb.velocity;
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        rb.AddForce(CalcForce() * strength);
    }
}
