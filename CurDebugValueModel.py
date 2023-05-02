class CurDebugValuesModel:
  NUM_OF_VALUES = 5
  def __init__ (self):
    self.debug_values = [0] * CurDebugValuesModel.NUM_OF_VALUES
  
  def update (self, debug_values):
    self.debug_values = debug_values
