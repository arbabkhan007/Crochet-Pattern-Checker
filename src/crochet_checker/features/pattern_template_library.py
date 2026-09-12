"""Pattern Template Library - Pattern templates"""
class PatternTemplateLibrary:
    def __init__(self):
        self.templates = {"basic_scarf": "Chain 20, sc across", "basic_hat": "Magic ring, inc 6 times"}
    
    def get_template(self, template_name: str) -> str:
        return self.templates.get(template_name, "Pattern not found")

if __name__ == "__main__":
    print("📚 Pattern Template Library - Working!")
    library = PatternTemplateLibrary()
    print(f"Scarf template: {library.get_template('basic_scarf')[:30]}...")
