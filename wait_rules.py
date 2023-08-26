class attribute_has_changed(object):
  def __init__(self, locator, val, attr):
    self.locator = locator
    self.val = val
    self.attr = attr

  def __call__(self, driver):
    element = driver.find_element(*self.locator)   # Finding the referenced element

    if self.attr == 'text':
        check_value = element.text
    else:
        check_value = element.get_attribute(self.attr)

    if self.val not in check_value:
        return element
    else:
        return False
