scripta
=======

scripta is a (untidy) collection of scripts that is supposed to perform repetitive operations from command line. Currently, it allows to perform the following operations:
* convert between matrices / networks representations from command line (adjacency list, adjacency matrix, edgelist) (some are TODOs).
* curb a matrix;
* calculate mutual information;
* normalize matrix (TODO)
* make a density plot.

The library needs numpy/matplotlib/scipy or the whole pylab environment.

Graph / matrix representations
------------------------------

### Edgelist
CSV file with the a line for each link, each line with the following
format

`src_label,dst_label[,weight]`

### Adjacency list
CSV file with a line for each node with outgoing links, each with following format

`src_label,dst1_label[:weight1],dst2_label[:weight2],...,dstN_label[:weightN]`

The separators `,` and `:` are generic and can be changed.

### Adjacency matrix
CSV file with a line for each node, and each line with a column for each
node, with the following format.

`[       , label1, label2, ..., labelN]`
`[label1], weight11, weight12, ..., weight1N]`
