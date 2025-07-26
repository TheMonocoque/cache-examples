#!/usr/bin/env python

class GDSF:
    def __init__(self, cache_size):
        self.cache_size = cache_size
        self.cache = {}  # Key: Page ID, Value: (count, last_access_time)
        self.time_counter = 0

    def access_page(self, page_id):
        if page_id in self.cache:
            # Update count and last access time for the accessed page
            self.cache[page_id] = (self.cache[page_id][0] + 1, self.time_counter)
        else:
            # If the cache is full, need to replace a victim page
            if len(self.cache) >= self.cache_size:
                # Find all pages in the cache and track their frequency and last access time
                candidates = list(self.cache.items())
                
                # Sort by frequency ascending (lowest first)
                sorted_by_freq = sorted(candidates, key=lambda x: x[1][0])
                
                # From the lowest frequency group, select the one with the oldest last access time
                min_freq = sorted_by_freq[0][1][0]
                freq_group = [(page, info) for page, info in candidates if info[0] == min_freq]
                
                # Sort by last access time ascending (oldest first)
                sorted_by_time = sorted(freq_group, key=lambda x: x[1][1])
                victim_page = sorted_by_time[0][0]
                
                # Remove the victim page from the cache
                del self.cache[victim_page]
                
            # Add the new page to the cache
            self.cache[page_id] = (1, self.time_counter)
        
        # Increment time counter for next operation
        self.time_counter += 1

def run_gdsf_cache_sim():
    cache_size = 3  # Number of frames in the cache
    page_sequence = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]  # Page access sequence
    
    gdsf = GDSF(cache_size)
    
    print("GDSF Cache Simulation")
    print("-----------------------")
    print(f"Cache Size: {cache_size}")
    print(f"Page Sequence: {page_sequence}")
    print("\nOperation | Cache State")
    print("-------------------------")
    
    for page in page_sequence:
        gdsf.access_page(page)
        current_cache = list(gdsf.cache.items())
        if current_cache:
            print(f"P{page} | {[item[0] for item in current_cache]}")
        else:
            print(f"P{page} | []")

    # Output the order of victim page replacements
    print("\nVictim Page Replacement Order:")
    # To track which pages were replaced, we can modify the access_page method to record this.
    # However, in the current implementation, we only know when a replacement occurs.
    # For simplicity, this example focuses on simulating the cache state rather than tracking replacements.


def main():
    print("Hello from cache-examples!")
    run_gdsf_cache_sim()


if __name__ == "__main__":
    main()
