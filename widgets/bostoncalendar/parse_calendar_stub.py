# We don't have caching yet, so stub out the stuff that hits any URLs.
from parse_calendar import CalendarEntry
# from menu import menuize, build_submenu
from bucket_schemas import boston_calendar_schema

_events = []
_events.append({"title":"Test item 1", "time":"Wednesday, May 02, 2018 07:00 A","location":"Nowhere", "calendar_url":"https://www.example.com"})
_events.append({"title":"Test item 2", "time":"Wednesday, May 02, 2018 07:00 P", "location":"Everywhere", "calendar_url":"https://www.asdf.com"})
_events.append({"title":"Test item 3", "time":"Wednesday, May 02, 2018 goes until 05/03", "location":"Anywhere", "calendar_url":"https://en.wikipedia.org"})
_events.append({"title":"Test item 4", "time":"Wednesday, May 02, 2018 06:00 P", "location":"Somewhere", "calendar_url":"https://www.html5zombo.com"})

#def build_calendar_items():
  #return [build_submenu("Boston Calendar", build_menu_contents(_events))]

# def build_menu_contents(events):
#   bucketing = boston_calendar_schema.bucketize(events)
#   bucketing_keys = bucketing.keys()
#   contents = []
#   for i in bucketing_keys:
#     if bucketing[i]:
#       contents.append([boston_calendar_schema.name(i), [e for e in bucketing[i]]])
#   return contents

def build_calendar_items():
  return """<menu>
    Boston Calendar
    <menu>
      Morning
      <item time="Wednesday, May 02, 2018 07:00 A" location="Nowhere" url="https://www.example.com" action="navigate">
        Test item 1
      </item>
    </menu>
    <menu>
      Evening
      <item time="Wednesday, May 02, 2018 06:00 P" location="Somewhere" url="https://www.html5zombo.com" action="navigate">
        Test item 4
      </item>
    </menu>
    <menu>
      Night
      <item time="Wednesday, May 02, 2018 07:00 P" location="Everywhere" url="https://www.asdf.com" action="navigate">
        Test item 2
      </item>
    </menu>
    <menu>
      Multi-Day
      <item time="Wednesday, May 02, 2018 goes until 05/03" location="Anywhere" url="https://en.wikipedia.org" action="navigate">
        Test item 3
      </item>
    </menu>
  </menu>"""