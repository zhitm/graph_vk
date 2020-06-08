from graph import Graph

if __name__ == '__main__':
	g = Graph()
	g.load_graph('components\members.txt')
	g.create_components_files()
