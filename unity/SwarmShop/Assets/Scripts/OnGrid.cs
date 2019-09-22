using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class OnGrid : MonoBehaviour
{
    private GridBehavior grid;
    // Start is called before the first frame update
    void Start()
    {
        Debug.Assert(transform.parent != null);
        GameObject parent = transform.parent.gameObject;
        grid = parent.GetComponent<GridBehavior>();
        Debug.Assert(grid != null);
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
