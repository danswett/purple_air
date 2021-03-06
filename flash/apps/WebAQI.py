"""Display AQI from purple air monitor."""
import aqi
from aqi_and_color import RGBStringToList 
import sys

CONFIG_FILE = 'aqi_web.json'
URL_TEMPLATE = 'https://www.purpleair.com/json?show={sensor_location}'


class PurpleWeb():
  """Device specific details."""

  def __init__(self):
    self.config_file = CONFIG_FILE
    self.url_template = URL_TEMPLATE
    self.pm2_5_atm = None
    self.pm2_5_cf_1 = None
    self.humidity = None
    self.seconds_between = 50

  def json_to_data(self, data):
    data_a = data['results'][0]
    data_b = data['results'][1]
    self.pm2_5_atm = (float(data_a['pm2_5_atm']) + float(data_b['pm2_5_atm']))/2
    self.pm2_5_cf_1 = (float(data_a['pm2_5_cf_1']) + float(data_b['pm2_5_cf_1']))/2
    self.aqi = -1
    self.color = [200, 200, 200]
    self.humidity = float(data_a['humidity'])



def main():
  """Main loop. Runs forever."""
  interface = PurpleWeb()
  my_aqi = aqi.AQI(interface)
  my_aqi.Run()
  sys.exit(1)
  while True:
    try:
      my_aqi.Run()
    except Exception as e:
      # Yes, I know that this is ugly, but it's for debugging bogies.
      print('Oops! Fell through: %s' % e)
      my_aqi.hw.WaitMS(10)

# The M5StickC doesn't use the name __main__, it uses m5ucloud.
if __name__ in ('__main__', 'm5ucloud'):
  main()
