# Understanding trie implementation with redis

## Trie Node
> Structure of a node

    class Node
        key: string
        count: int
        end: bool
        keys: map<string, int>

## Trie Node Root
> Entry point

    root = map<Node, int>

## Insert function
> To insert a new word in vocabulary

    function insert(word)
        for index [ 0 -> word.length ]
            key = word[ 0 -> index ]
            
            if key == word (if reached the last character)
                if key exists in root
                    increment root.key.count
                else
                    set root.key.count = 1
                    set root.key.end = true
                    
            else
                next_key = word[ 0 -> index + 1 ] (the following character)
                
                if key exists in root
                    increment root.key.count

                    if next_key exists in root.key.keys
                        increment root.key.keys.next_key
                    else
                        set root.key.keys.next_key = 1
                
                else
                    set root.key.count = 1
                    set root.next_key.count = 1
                    set root.key.keys.next_key = 1

## Search function
> To search all words with prefix best match with `query`

    function search(query)
        for index [ query.length -> 0 ] (decrementing index)
            key = query[ 0 -> index ]

            if key exists in root
                results = list<string>
                return helper(key, results)
    
    function helper(key, results)
        if root.key.end == true
            results.append(key)
            return results
        
        for child_key in root.key.keys
            results = helper(child_key, results)
        
        return results