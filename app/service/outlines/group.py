from dataclasses import dataclass, field

from .bible import BibleService
from .chapter import ChapterService
from .substory import SubstoryService


@dataclass(slots=True)
class OutlineServiceGroup:
    bible: BibleService = field(default_factory=BibleService)
    substory: SubstoryService = field(default_factory=SubstoryService)
    chapter: ChapterService = field(default_factory=ChapterService)
