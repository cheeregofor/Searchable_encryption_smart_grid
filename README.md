# Searchable_encryption_smart_grid
This is the code of a searchable encryption scheme on smart grid data.

**1.run the build_index.py**

Please input the file to be encrypted: 8000_data.csv

Please input the file stored the master key: masterkey

Please input the file stores keyword name: dataname_list

Then we get the index file named 8000_data_index.csv.



**2.run the build_trapdoor.py**

Please input the keyword you want to search: Wheeling Power Co

Please input the file stored the master key: masterkey

Then we get the trapdoor file named Wheeling Power Co_trapdoor.


**3.run the search.py**

Please input the trapdoor file: Wheeling Power Co_trapdoor

Please input the index file: 8000_data_index.csv

Then we get the search result.


**4.run the ID_hash_dict.py**

Please input the search results: 1af3254fd723ed530263aca30c0a08c3,012d8d02496ecee17b6f3c840c51ddcc,4d6412c65a4f17de2e715d2da87a3f94,d6ea773978a8487490a2613207391e6c,02039a1d0e79eb6d7dd9421f9e6c10a8,3a98eeb0e6d37e18568d67309d8acb9e,d69d41bb1f8743746302414325c85821,86eefd1bac5837a9c26a7e5956f5be77,fade291b4096c1b2c67940295968eb77,c7525e6edd79bf091ab3d522dcf9c90a,108902221659cdcd6de59ce37369779d

Then we get the final result: 2123,3545,6397,4967,4256,5682,1412,7827,2834,701,7112.
