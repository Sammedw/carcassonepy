    
        elif __name__ == "__main__":
            # divide iterations between number of trees
            #print("divide")
            tree_iterations = int(self.iterations / self.trees)
            # start trees
            processes = []
            root_queue = Queue()
            for _ in range(self.trees):
                process = Process(target=self.uct_search, args=(self.game, next_tile, tree_iterations, root_queue))
                processes.append(process)
                process.start()
                #print("start tree")
            
            # iterate over all tree roots
            root = root_queue.get()
            #print("collect roots")
            for _ in range(self.trees - 1):
                #print("get root")
                next_root = root_queue.get()
                # combine visit and reward stastics
                for i, child in enumerate(next_root.children):
                    root.children[i].visit_count += child.visit_count
                    root.children[i].total_reward += child.total_reward
            
            # close processes
            #print(processes)
            for process in processes:
                #print(process)
                process.join()
                #print("close tree")