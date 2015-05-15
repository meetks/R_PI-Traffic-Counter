Last login: Fri May 15 10:28:33 on ttys000
KGUNJIKA-M-60LS:~ kshitijgunjikar$ cd ~/Downloads/counter
KGUNJIKA-M-60LS:counter kshitijgunjikar$ ls
8188eu-20140616.tar.gz	carlog			pi_car_counter.tgz
8188eu.ko		counter.tar.gz		python_games
Desktop			ocr_pi.png		test_log
car_counter.tar.gz	pi_car_counter
KGUNJIKA-M-60LS:counter kshitijgunjikar$ cd pi_car_counter
KGUNJIKA-M-60LS:pi_car_counter kshitijgunjikar$ ls
spidev
KGUNJIKA-M-60LS:pi_car_counter kshitijgunjikar$ cd spidev/
KGUNJIKA-M-60LS:spidev kshitijgunjikar$ ls
adafruit_mcp3008.py	ifupdown-wlan.sh	spidev_test.c
car_counter.bak		rtc-pi			test.py
car_counter.py		spi
KGUNJIKA-M-60LS:spidev kshitijgunjikar$ vim spidev_test.c 








167         /*
168          * spi mode
169          */
170         ret = ioctl(fd, SPI_IOC_WR_MODE, &mode);
171         if (ret == -1)
172                 pabort("can't set spi mode");
173 
174         ret = ioctl(fd, SPI_IOC_RD_MODE, &mode);
175         if (ret == -1)
176                 pabort("can't get spi mode");
177 
178         /*
179          * bits per word
180          */
181         ret = ioctl(fd, SPI_IOC_WR_BITS_PER_WORD, &bits);
182         if (ret == -1)
183                 pabort("can't set bits per word");
184 
185         ret = ioctl(fd, SPI_IOC_RD_BITS_PER_WORD, &bits);
186         if (ret == -1)
187                 pabort("can't get bits per word");
188 
189         /*
190          * max speed hz
191          */
192         ret = ioctl(fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed);
193         if (ret == -1)
194                 pabort("can't set max speed hz");
195 
196         ret = ioctl(fd, SPI_IOC_RD_MAX_SPEED_HZ, &speed);
197         if (ret == -1)
198                 pabort("can't get max speed hz");
199 
200         printf("spi mode: %d\n", mode);
201         printf("bits per word: %d\n", bits);
202         printf("max speed: %d Hz (%d KHz)\n", speed, speed/1000);
203 
204         transfer(fd);
205 
206         close(fd);
207 
208         return ret;
209 }

