using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Rigidbody))]
public class BoidfriendBehavior : MonoBehaviour
{
    public GameObject boundingCube;
    Rigidbody rb;
    void Start()
    {
        rb = GetComponent<Rigidbody>();
        rb.velocity = Random.onUnitSphere * 5;
    }

    void FixedUpdate()
    {
        // move forward
        // look at where we're going
        if(rb.velocity.sqrMagnitude > 0f)
        {
            transform.rotation = Quaternion.LookRotation(rb.velocity, Vector3.up);
        }

        float xmin, xmax, ymin, ymax, zmin, zmax;
        Vector3 pos = boundingCube.transform.position;
        float length = boundingCube.transform.lossyScale.x;
        float width = boundingCube.transform.lossyScale.z;
        float height = boundingCube.transform.lossyScale.y;
        xmin = pos.x - length / 2f;
        xmax = pos.x + length / 2f;
        zmin = pos.z - width / 2f;
        zmax = pos.z + width / 2f;
        ymin = pos.y - height / 2f;
        ymax = pos.y + height / 2f;

        if(transform.position.x < xmin)
        {
            transform.position = new Vector3(xmax, transform.position.y, transform.position.z);
        }
        if(transform.position.x > xmax)
        {
            transform.position = new Vector3(xmin, transform.position.y, transform.position.z);
        }

        if(transform.position.y < ymin)
        {
            transform.position = new Vector3(transform.position.x, ymax, transform.position.z);
        }
        if(transform.position.y > ymax)
        {
            transform.position = new Vector3(transform.position.x, ymin, transform.position.z);
        }

        if(transform.position.z < zmin)
        {
            transform.position = new Vector3(transform.position.x, transform.position.y, zmax);
        }
        if(transform.position.z > zmax)
        {
            transform.position = new Vector3(transform.position.x, transform.position.y, zmin);
        }
    }
}
