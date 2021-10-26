#include "struct.h"

struct Edge {
    struct Vertex *vertex;
    struct Edge *next;
    double p;
};

struct Vertex {
    int id;
    struct Edge *first_edge;   
};

struct Graph {
    struct Vertex *vertex_list;
    int vertex_number;
};