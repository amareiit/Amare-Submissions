instance_type      = "t3.micro"
key_name           = "module05-key"
security_group_ids = ["sg-05216bd7ab19514d7"]
instance_count     = 3
user_data          = "install-env.sh"
tags               = "module-05"
