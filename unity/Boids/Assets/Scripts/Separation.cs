using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(FieldOfView))]
[RequireComponent(typeof(Rigidbody))]
public class Separation : MonoBehaviour
{
    public float strength = 10f;
    Rigidbody rb;
    FieldOfView fov;
    // Start is called before the first frame update
    void Start()
    {
        rb = GetComponent<Rigidbody>();
        fov = GetComponent<FieldOfView>();
    }

    Vector3 CalcForce()
    {
        List<GameObject> boidObjs = fov.GetVisibleBoids();
        Vector3 resultant = new Vector3();
        foreach (GameObject boid in boidObjs)
        {
            Vector3 disp = boid.transform.position - transform.position;
            if(disp.magnitude != 0)
            {
                    Vector3 force = disp * -1f / disp.sqrMagnitude;
                    resultant += force;
            }
        }
        return resultant;
    }

    void FixedUpdate()
    {
        rb.AddForce(CalcForce() * strength);
    }
}
