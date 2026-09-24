"""Stitch Consumer - Processes stitch instructions"""
class StitchConsumer:
    def consume(self, stitch_type: str, count: int):
        return {'stitch': stitch_type, 'count': count}
