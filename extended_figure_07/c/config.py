class Neckmimic:
  neckmimic_range = range(7884, 7898+1)
  resname_dict = {
      resid: f'{char}{index}'
      for resid, index, char in zip(
        range(7884, 7898+1),
        range(671,685+1),
        "KMTKAKRNRYLNNSV",
        )
    }
