#!/bin/bash
# redirect permanent
if (( "$(pgrep -c nginx)" > 0)); then
	echo "Nginx server already installed & running"
	echo "Now adding redirect_me"
	echo "server {
			listen 80 default_server;
			listen [::]:80 default_server;

			root /var/www/html;
			# Add index.php to the list if you are using PHP
			index index.html index.htm index.nginx-debian.html;

			server_name _;
			
			error_page 404 /custom_404.html;
			location /custom_404.html {
				root /var/www/html/;
				internal;
			}

			rewrite ^/redirect_me https://www.youtube.com/watch?v=QH2-TGUlwu4/ permanent;

			location /hbnb_static/ {
				alias /data/web_static/current/;
				index index.html;
			}

		}" | sudo tee /etc/nginx/sites-available/default > /dev/null
		echo "Ceci n'est pas une page" | sudo tee /var/www/html/custom_404.html > /dev/null
		echo "Adding symlink.."
		sudo ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default
		echo "redirect_me done succesfully"
		echo "Reloading Nginx server..."
		sudo nginx -s reload
	else
		echo "cleaning..."
		sudo apt-get --remove purge nginx nginx-common nginx-core -y > /dev/null
		sudo apt-get -y autoremove > /dev/null
		sudo apt-get -y autoclean > /dev/null
		echo "updating apt-get cache.."
		sudo apt-get -y update > /dev/null
		echo "working on dependencies, nginx-common & nginx-core"
		sudo apt-get install -y nginx-common nginx-core
		sudo apt-get install -y nginx > /dev/null
		echo "Hello World!" | sudo tee /var/www/html/index.html
		echo "Starting server..."
		sudo service start
		sudo ./3-redirection
fi
echo "Creating a directory /data/ if it does not exist..."
sudo mkdir -p /data/web_static/releases/test/ /data/web_static/shared/

# Create the folders if they don't exist
sudo mkdir -p /data/web_static/releases/ /data/web_static/

# Create the fake HTML file
echo "<html><body><h1>Hello, this is a test index.html file!</h1></body></html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null
echo "Done!"
echo "Creating a symlink ... "
if [ -L "/data/web_static/current" ]; then
	sudo rm -f /data/web_static/current
fi

sudo ln -s /data/web_static/releases/test/ /data/web_static/current
echo "Symbolic link created: /data/web_static/current -> /data/web_static/releases/test/"
sudo chown -R ubuntu:ubuntu /data/
echo "All configuration set now reloading nginx server..."
sudo nginx -s reload
echo "Good to go!"
