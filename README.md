#Aws job manager

###commands:
1.`make run` should init the application http://localhost:8888
2. `make smoke` runs entire tests


    Aws async job/tasks managing , handling responses
    
    1. Create kineses stream AwsJobManager
    2. Once the stream is ready- checks if process didnt failed
    3.put some data into the stream - put records. 
    4.read records from an S3 file, with generated filename
    5. Apply some kind of processing on the data read (whatever you like) and
        write the result file to S3. 
    6. Client checks if exists by 400 response generated s3 link url