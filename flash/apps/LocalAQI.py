"""Display AQI from purple air monitor."""
import aqi
from aqi_and_color import RGBStringToList 
import sys

CONFIG_FILE = 'aqi.json'
URL_TEMPLATE = 'http://{sensor_location}/json?live=false'


class PurpleLocal():
  """Interface specific details for local web."""

  def __init__(self):
    self.config_file = CONFIG_FILE
    self.url_template = URL_TEMPLATE
    self.pm2_5_atm = None
    self.pm2_5_cf_1 = None
    self.humidity = None
    self.seconds_between = 10

  def json_to_data(self, data):
    self.pm2_5_atm = (data['pm2_5_atm'] + data['pm2_5_atm_b'])/2
    self.pm2_5_cf_1 = (data['pm2_5_cf_1'] + data['pm2_5_cf_1_b'])/2
    self.aqi = (data['pm2.5_aqi'] + data['pm2.5_aqi_b'])/2
    rgb = RGBStringToList(data['p25aqic'])
    rgb_b = RGBStringToList(data['p25aqic_b'])
    self.color = [(int(c[0])+int(c[1]))/2 for c in zip(rgb, rgb_b)]
    self.humidity = data['current_humidity']



def main():
  """Main loop. Runs forever."""
  interface = PurpleLocal()
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
