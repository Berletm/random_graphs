#include <iostream>
#include <vector>
#include <random>
#include <set>

static std::random_device rd;

static std::mt19937 generator(rd());

static std::uniform_real_distribution<float> uniform_dist(0.0f, 1.0f);

static size_t n_vertices = 5;

static size_t n_edges = 0;

static float prob = 0.5f;

using adj_matrix = std::vector<std::vector<bool>>;

class Graph
{
public:
    void print_matrix()
    {
        for (size_t i = 0; i < n_vertices; ++i)
        {
            for (size_t j = 0; j < n_vertices; ++j)
            {
                std::cout << this->graph[i][j] << " ";
            }
            std::cout << std::endl;
        }
    }

    void add_edge(size_t u, size_t v)
    {
        this->graph[u][v] = true;
        this->graph[v][u] = true;
    }

    adj_matrix& get_graph()
    {
        return this->graph;
    }

private:
    adj_matrix graph{n_vertices, std::vector<bool>(n_vertices, false)};
};

void dfs(int v, adj_matrix& graph, std::vector<bool>& visited) 
{
    visited[v] = true;
    for (size_t u = 0; u < graph.size(); ++u) 
    {
        if (graph[v][u] && !visited[u])
        {
            dfs(u, graph, visited);
        }
    }
}

size_t count_components(Graph& graph)
{   
    adj_matrix& matrix = graph.get_graph();
    std::vector<bool> visited(n_vertices, false);
    int components = 0;
    
    for (int i = 0; i < n_vertices; ++i) 
    {
        if (!visited[i])
        {   
            dfs(i, matrix, visited);
            components++;
        }
    }
    
    return components;
}

bool generate_edge()
{
    return uniform_dist(generator) <= prob? 1: 0;
}

void build_graph(Graph& graph) 
{
    if (n_vertices == 0) return;

    auto& adj_mat = graph.get_graph();
    std::uniform_int_distribution<size_t> uni_int_dist(0, n_vertices - 1);
    std::set<std::pair<size_t, size_t>> used_edges;

    while (used_edges.size() < n_vertices * (n_vertices - 1) / 2) 
    {
        size_t u = uni_int_dist(generator);
        size_t v = uni_int_dist(generator);
        
        if (u == v) continue;
        
        if (u > v) std::swap(u, v);
        
        if (used_edges.count({u, v}) > 0) continue;
        
        if (generate_edge()) 
        {
            graph.add_edge(u, v);
            n_edges += 1;
        }
        used_edges.insert({u, v});
    }
}

int main(int argc, char* argv[])
{   
    if (argc >= 3)
    {
        n_vertices = atoi(argv[1]);
        prob = atof(argv[2]);
    }

    Graph my_graph;

    build_graph(my_graph);

    size_t n_components = count_components(my_graph);

    std::cout << n_components << ' ';

    std::cout << n_edges << ' ';

    std::cout << n_edges - n_vertices + n_components << std::endl;

    return 0;
}