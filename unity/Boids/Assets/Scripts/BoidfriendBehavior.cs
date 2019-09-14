using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Rigidbody))]
public class BoidfriendBehavior : MonoBehaviour
{
    Rigidbody rb;
    void Start()
    {
        rb = GetComponent<Rigidbody>();
        rb.velocity = Random.onUnitSphere;
    }

    void FixedUpdate()
    {
        // move forward
        // look at where we're going
        if(rb.velocity.sqrMagnitude > 0f)
        {
            transform.rotation = Quaternion.LookRotation(rb.velocity, Vector3.up);
        }
    }
}
