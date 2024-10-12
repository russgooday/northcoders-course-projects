// CPython Module implementation of heapify
#include <Python.h>
#include <stdio.h>

#define left_child(i) ((i << 1) + 1)
#define parent_of(i) ((i - 1) >> 1)
#define len(x) sizeof(x) / sizeof(x[0])
#define _PyList_ITEMS(op) _Py_RVALUE(_PyList_CAST(op)->ob_item)


/* Min heapify a list in place */
static void min_heapify(PyObject *heap, Py_ssize_t pos) {
    PyObject *temp; 
    PyObject **arr = _PyList_ITEMS(heap);
    Py_ssize_t heap_size = PyList_Size(heap);
    Py_ssize_t parent = pos;
    Py_ssize_t right_pos;
    pos = left_child(pos);

    while (pos < heap_size) {
        right_pos = pos + 1;

        if (right_pos < heap_size && PyObject_RichCompareBool(arr[right_pos], arr[pos], Py_LE)) {
            pos = right_pos;
        }

        if (PyObject_RichCompareBool(arr[pos], arr[parent], Py_LT)) {
            temp = arr[pos];
            arr[pos] = arr[parent];
            arr[parent] = temp;
            parent = pos;
            pos = left_child(pos);
            continue;
        }
        break;
    }
}


/* Heapify a list in place */
static void heapify(PyObject *heap) {
    Py_ssize_t heap_size = PyList_Size(heap);
    Py_ssize_t i = 1 + parent_of(heap_size);

    for (; i-- > 0;) {
        min_heapify(heap, i);
    }
}


/* Replaces the root of the heap with a given value and return the smallest element */
static PyObject* heap_replace(PyObject *heap, PyObject *val) {
    // Get the smallest element from the heap (first element)
    PyObject *smallest = PyList_GET_ITEM(heap, 0);

    Py_INCREF(smallest);
    Py_INCREF(val);
    // Set the new value at position 0 in the list
    PyList_SET_ITEM(heap, 0, val);

    min_heapify(heap, 0);

    return smallest;  // Return the original smallest element
}


static PyObject* api_heap_replace(PyObject* module, PyObject *const *args, Py_ssize_t nargs) {
    if (nargs < 2) {
        PyErr_SetString(PyExc_TypeError, "function expects at least 2 positional arguments");
        return NULL;
    }

    if (!PyList_Check(args[0])) {
        _PyArg_BadArgument("heapreplace", "argument 1", "list", args[0]);
        return NULL;
    }

    return heap_replace(args[0], args[1]);
}


static PyObject* api_heapify(PyObject* module, PyObject *const *args, Py_ssize_t nargs) {
    if (nargs < 1) {
        PyErr_SetString(PyExc_TypeError, "function expects at least 1 positional argument");
        return NULL;
    }

    if (!PyList_Check(args[0])) {
        _PyArg_BadArgument("heapify", "argument 1", "list", args[0]);
        return NULL;
    }

    heapify(args[0]);
    Py_RETURN_NONE;
}


/* Method definitions */
static PyMethodDef HeapMethods[] = {
    {   "heapify", 
        _PyCFunction_CAST(api_heapify), 
        METH_FASTCALL, 
        "Heapify a list in place."
    },
    {
        "heap_replace", 
        _PyCFunction_CAST(api_heap_replace), 
        METH_FASTCALL, 
        "Replace the root of the heap with a given value and return the smallest element."
    },
    {NULL, NULL, 0, NULL}
};

/* Module definition */
static struct PyModuleDef heapmodule = {
    PyModuleDef_HEAD_INIT,
    "heap",        /* name of module */
    NULL,          /* module documentation */
    -1,            /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables */
    HeapMethods
};

/* Module initialization */
PyMODINIT_FUNC PyInit_heap(void) {
    return PyModule_Create(&heapmodule);
}
