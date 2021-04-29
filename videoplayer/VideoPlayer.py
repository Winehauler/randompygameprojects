import cv2 as cv
import pygame


def crop_frame(frame, topleft, bottomright):
    tl, br = topleft, bottomright
    frame = frame[tl[0]:br[0],tl[1]:br[1]]
    return frame


class VideoPlayer:


    def __init__(self, filename, shape=None, keep_ratio=True):
        self._shape = list(shape) if shape is not None else None
        self.keep_ratio = keep_ratio
        self.filename = filename

        self.capture = cv.VideoCapture(filename)
        self.num_frames = self._count_frames()


    def _count_frames(self):
        return self.capture.get(cv.CAP_PROP_FRAME_COUNT)


    def set_crop(self, topleft, bottomright):
        self._crop = (topleft, bottomright)


    def unset_crop(self):
        self._crop = False


    def get_frame(self, position=None):
        if not position is None:
            self.capture.set(1, position)
        succ, frame = self.capture.read()
        if not succ:
            return False
        if hasattr(self, '_crop') and not self._crop is False:
            frame = crop_frame(frame, *self._crop)
        cv.cvtColor(frame, cv.COLOR_BGR2RGB, frame)

        
        shape = frame.shape[:2]
        frame_surface = pygame.Surface(shape)
        pygame.surfarray.blit_array(frame_surface, frame)
        
        frame_surface = pygame.transform.rotate(frame_surface, -90)
        frame_surface = pygame.transform.flip(frame_surface, 1, 0)

        _shape = None if self._shape is None else self._shape[:]
        if _shape is not None:
            if self.keep_ratio:
                max_i = _shape.index(max(_shape))
                ratio = min(shape) / max(shape)
                _shape[max_i] = ratio * _shape[1 - max_i]
                _shape = [int(s) for s in _shape]
            
            frame_surface = pygame.transform.scale(frame_surface, _shape)
            
        return frame_surface

