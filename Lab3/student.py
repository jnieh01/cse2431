
import threading

# =======================================================================================================
# This is the producer thread function.  
# It reads items from f_in (which points to the already opened file INPUT_FILE), and 
# places the read item into the bounded buffer at location IN (e.g., buffer[IN]).
#
# producer_num:  the id of the thread running the function
# f_in:          open file handle to INPUT_FILE
# buffer:        buffer class object, already created
# locks:         set of locks, already created

def student_producer(producer_num, f_in, buffer, locks):
    # The buffer.py code catches a terminal kill signal, and sets buffer.KILL so producers/consumers see it and stop.
    # Students do NOT need to write any code to handle these interrupts.
    while not buffer.KILL:    

        # ------ PLACE YOUR PRODUCER CODE BELOW THIS LINE ------
        #
        # You will need additional lines of code around (and possibly between) those provided below to implement
        # appropriate locking and an exit/return to break out of the main 'while' loop.
        #
        # You will need to access, set, and/or use parts of the passed in buffer and its components.  Be sure
        # to read the buffer class definition and its corresponding comments at the top of buffer.py
        #
        # In this function, use the following locks provided in the 'locks' parameter (which is defined near the top of buffer.py):
        #   - locks.producer_file_in
        #   - locks.producer_buffer
        #   - You must appropriately use both producer locks listed above to receive full credit.
        #
        # Please note: 
        #   - You must NOT use python 'with lock' statements.
        #   - You must use acquire() and release() explicitly.  That is, calls like:
        #          locks.producer_file_in.acquire() 
        #          locks.producer_file_in.release()
        #   - While you may add code in and around the labeled P-# lines below, do NOT edit or re-order the P-# lines.  
        #     Changes to those lines will break the tests and grading code.

        locks.producer_file_in.acquire() 
        line = f_in.readline()                                             # Read a line of data from f_in into the variable 'line'     
        # print(f"nieh-1: producer-{producer_num} read {line.strip()}")
        locks.producer_file_in.release()
        
        if line == "": 
            return
        try:              item  = int(line)                                # LINE P-1:  DO NOT CHANGE OR REORDER THIS LINE RELATIVE TO P-# LABELED LINES!  Turns the read input line into an integer 'item'
        except Exception: item  = 0                                        # LINE P-2:  DO NOT CHANGE OR REORDER THIS LINE RELATIVE TO P-# LABELED LINES!  If input item bad, sets to invalid.  With good code, this shouldn't happen.  (e.g., shouldn't try to use data beyond end of file)
        
        
        
        locks.producer_buffer.acquire()



        # wait consumer 
        while ((buffer.IN + 1) % buffer.NUM_SLOTS) == buffer.OUT :
            pass
        
     
        # print(f"nieh-2: producer-{producer_num} item {item}")
        buffer.ITEMS[buffer.IN] = (item, producer_num)                     # LINE P-3:  DO NOT CHANGE OR REORDER THIS LINE RELATIVE TO P-# LABELED LINES!  Inserts a 2-part tuple into buffer.   
        buffer.IN = (buffer.IN + 1) % buffer.NUM_SLOTS
        locks.producer_buffer.release()

        # ------ PLACE YOUR PRODUCER CODE ABOVE THIS LINE ------

# ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ 





# =======================================================================================================
# This is the consumer thread function.  
# It reads items from the bounded buffer at location OUT (e.g., buffer[OUT]) and 
# writes the output item to f_out (which points to the already opened file OUTPUT_FILE)
#
# consumer_num:  the id of the thread running the function
# f_out:         open file handle to OUTPUT_FILE
# buffer:        buffer class object, already created
# locks:         set of locks, already created

def student_consumer(consumer_num, f_out, buffer, locks):
    # The buffer.py code catches a terminal kill signal, and sets buffer.KILL so producers/consumers see it and stop.
    # Students do NOT need to write any code to handle these interrupts.
    while not buffer.KILL:

        # ------ PLACE YOUR CONSUMER CODE BELOW THIS LINE ------
        #
        # You will need additional lines of code around (and possibly between) those provided below to implement
        # appropriate locking and an exit/return to break out of the main 'while' loop.
        #
        # You will need to access, set, and/or use parts of the passed in buffer and its components.  Be sure
        # to read the buffer class definition and its corresponding comments at the top of buffer.py
        #
        # Don't forget to use buffer.PRODUCERS_DONE in this function.  It's set for you after the producer threads are done.
        #
        # In this function, use the following locks provided in the 'locks' parameter (which is defined near the top of buffer.py):
        #   - locks.consumer_buffer
        #   - locks.consumer_file_out
        #   - You must appropriately use both consumer locks listed above to receive full credit.
        #
        # Please note: 

        #   - You must NOT use python 'with lock' statements.
        #   - You must use acquire() and release() explicitly.  That is, calls like:
        #          locks.consumer_buffer.acquire() 
        #          locks.consumer_buffer.release()
        #   - While you may add code in and around the labeled C-# lines below, do NOT edit or re-order the C-# lines.  
        #     Changes to those lines will break the tests and grading code.

        
        locks.consumer_buffer.acquire()
        
        while buffer.IN == buffer.OUT:                                             # Buffer empty, consumer wait
            if buffer.PRODUCERS_DONE:
                locks.consumer_buffer.release()
                return

        
        try:              (item, producer_num) = buffer.ITEMS[buffer.OUT]          # LINE C-1:  DO NOT CHANGE OR MOVE THIS LINE RELATIVE TO C-# LABELED LINES!  Pulls a 2-part tuple out of buffer.
        except Exception: (item, producer_num) = (0, 0)                            # LINE C-2:  DO NOT CHANGE OR MOVE THIS LINE RELATIVE TO C-# LABELED LINES!  Sets the tuple to 'invalid' info if bad data pulled from buffer.
        print(f"nieh-3: consumer-{consumer_num} read {item}")

        buffer.OUT = (buffer.OUT + 1) %  buffer.NUM_SLOTS       
        
        locks.consumer_buffer.release()


        locks.consumer_file_out.acquire()         
        f_out.write('%d\t%d\t%d\n' % (item, producer_num, consumer_num))          # LINE C-3:  DO NOT CHANGE OR MOVE THIS LINE RELATIVE TO C-# LABELED LINES!  Writes a 3-part 'tuple' (really, tab-separated data) to f_out.
        print(f"nieh-4: consumer-{consumer_num} write {item}")
        locks.consumer_file_out.release()

        # if buffer.PRODUCERS_DONE and buffer.IN == buffer.OUT:                     # Return if all producers finsihed
        #     return

        # ------ PLACE YOUR CONSUMER CODE ABOVE THIS LINE ------


# ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ 


