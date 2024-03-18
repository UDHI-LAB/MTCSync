import json
import re

class INTEGRATOR:
  def __init__(self, *, scenario_path, lighting_paths) -> None:
    with open(scenario_path, "r", encoding="utf-8") as f:
      scenario: str = f.read()

    re_scenario: str = re.sub(r'/\*[\s\S]*?\*/|//.*', '', scenario)
    self.scenario: dict = json.loads(re_scenario)

    self.lighting: list[dict] = []
    for path in lighting_paths:
      with open(path, "r", encoding="utf-8") as f:
        lighting: str = f.read()

      re_lighting: str = re.sub(r'/\*[\s\S]*?\*/|//.*', '', lighting)
      self.lighting.append(json.loads(re_lighting))

    self.program_lighting: dict[list[str]] = {p["id"]: [] for p in self.scenario["playlist"]}

    for num, lighting in enumerate(self.lighting):
      self.program_lighting[lighting["header"]["programID"]].append(num)


  def integration(self) -> dict:
    integrated: dict = {}

    integrated["header"] = self.scenario["header"]
    integrated["config"] = self.scenario["config"]
    integrated["playlist"] = [{"name": p["name"], "time": p["time"]} for p in self.scenario["playlist"]]

    integrated["timeline"] = self.scenario["timeline"]

    for p in self.program_lighting.keys():
      for num in self.program_lighting[p]:
        playlist_pos: int = [i for i, sp in enumerate(self.scenario["playlist"]) if sp["id"] == p][0]
        integrated["timeline"].extend(self._lighting_timeline_normalization(num, self.scenario["playlist"][playlist_pos]["time"]))

    integrated["timeline"] = self._timeline_sort(self._timeline_compression(integrated["timeline"]))

    return integrated


  def _timeline_sort(self, timeline: list[dict]) -> list[dict]:
    return sorted(timeline, key=lambda x: x["time"])


  def _timeline_compression(self, timeline: list[dict]) -> list[dict]:
    compressed: list[dict] = []

    for t in timeline:
      if (i := self._find([c["time"] for c in compressed], t["time"])) != -1:
        compressed[i].update(t)
        continue

      compressed.append(t)

    return compressed

  def _find(self, l: list, x: str) -> int:
    if x in l:
      return l.index(x)

    return -1

    
  def _lighting_timeline_normalization(self, lighting_num: int, start_time: str) -> dict:
    normalized: list = []

    timeline: list[dict] = self.lighting[lighting_num]["timeline"]
    config_id: str = self.lighting[lighting_num]["header"]["configID"]

    for t in timeline:
      start_hour, start_minute, start_second, start_frame = [int(x) for x in start_time.split(":")]
      lighting_hour, lighting_minute, lighting_second, lighting_frame = [int(x) for x in t["time"].split(":")]

      # とりあえずフレームは無視

      second = (start_second + lighting_second) % 60
      add_minute = (start_second + lighting_second) // 60

      minute = (start_minute + lighting_minute + add_minute) % 60
      add_hour = (start_minute + lighting_minute + add_minute) // 60

      # 24時間は超えないと仮定
      hour = start_hour + lighting_hour + add_hour

      n: dict = {}
      n["time"] = f"{hour:02d}:{minute:02d}:{second:02d}:{start_frame:02d}"
      n[config_id] = self._get_order(lighting_num, t["order"])

      normalized.append(n)

    return normalized


  def _get_order(self, lighting_num, order: str) -> str:
    keys = order.split(".")

    order: str | dict = self.lighting[lighting_num]["order"][keys[0]]

    if isinstance(order, str):
      return order

    for key in keys[1:]:
      order = order[key]

    if not isinstance(order, str):
      print(f"error: {order} is not string")
      return ""

    return order

if __name__ == "__main__":
  print("test")
  print("input scenario path")
  scenario_path: str = input(">")
  print("input lighting paths(with comma, ex: lighting1.json,lighting2.json,...)")
  lighting_paths: list[str] = input(">").split(",")
  print("input output path")
  output_path: str = input(">")

  integrator: INTEGRATOR = INTEGRATOR(scenario_path=scenario_path, lighting_paths=lighting_paths)

  with open(output_path, "w", encoding="utf-8") as f:
    f.write(json.dumps(integrator.integration(), indent=2, ensure_ascii=False))