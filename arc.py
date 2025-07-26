class ARC:
    def __init__(self, size):
        self.size = size
        self.cache = {}  # Key: page ID, Value: (count, last_access_time)
        self.hit_count = 0
        self.miss_count = 0
        self.alpha = 0.5  # Initial alpha value
        self.time_counter = 0

    def access(self, page_id):
        if page_id in self.cache:
            current_info = self.cache[page_id]
            new_count = current_info[0] + 1
            self.cache[page_id] = (new_count, self.time_counter)
            self.hit_count += 1
        else:
            # Cache miss; need to add or replace
            if len(self.cache) < self.size:
                self.cache[page_id] = (1, self.time_counter)
                self.miss_count += 1
            else:
                victim = self.select_victim()
                del self.cache[victim]
                self.cache[page_id] = (1, self.time_counter)
                self.miss_count += 1

        # Update time counter for next access
        self.time_counter += 1

    def select_victim(self):
        candidates = list(self.cache.items())
        scores = []
        for page, info in candidates:
            freq = info[0]
            recency = self.time_counter - info[1]
            score = (freq ** self.alpha) * (recency ** (1 - self.alpha))
            scores.append((page, score))

        min_score = min(score for _, score in scores)
        victims = [page for page, score in scores if score == min_score]

        # For demonstration purposes, choose the first victim
        return victims[0]

    def get_cache_state(self):
        return list(self.cache.keys())

# Example usage:
if __name__ == "__main__":
    cache_size = 3
    page_sequence = [1, 2, 3, 4, 3, 3, 3, 1, 2, 5, 1, 2, 3, 4, 5]

    arc_cache = ARC(cache_size)

    print("Adaptive Replacement Cache (ARC) Simulation")
    print("-------------------------------------------")
    print(f"Cache Size: {cache_size}")
    print(f"Page Access Sequence: {page_sequence}")
    print("\nAccess Number | Page Accessed | Cache State | Alpha Value")
    print("------------------------------------------------------------")

    for i, page in enumerate(page_sequence):
        arc_cache.access(page)
        state = arc_cache.get_cache_state()
        if len(state) < cache_size:
            display_cache = f"[{', '.join(map(str, state))}]"
        else:
            display_cache = f"{{ {', '.join(map(str, sorted(state)))} }}"
        alpha = arc_cache.alpha
        print(f"{i + 1}          {page}       {display_cache}         {alpha:.2f}")

    # Additional information about hits and misses
    total_accesses = len(page_sequence)
    hit_rate = (arc_cache.hit_count / total_accesses) * 100 if total_accesses != 0 else 0
    print(f"\nTotal Accesses: {total_accesses}")
    print(f"Hit Count: {arc_cache.hit_count}")
    print(f"Miss Count: {arc_cache.miss_count}")
    print(f"Hit Rate: {hit_rate:.2f}%")
