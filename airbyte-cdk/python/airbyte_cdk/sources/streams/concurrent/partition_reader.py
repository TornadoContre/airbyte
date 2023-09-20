#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#

from queue import Queue
from typing import Optional

from airbyte_cdk.sources.streams.partitions.partition import Partition
from airbyte_cdk.sources.streams.record import Record


class PartitionReader:
    def __init__(self) -> None:
        self._output_queue: Queue[Record] = Queue()
        self._done = True

    def process_partition(self, partition: Partition) -> None:
        """
        Process a partition and put the records in the output queue.
        This method is meant to be called from a thread.
        :param partition:
        :return:
        """
        self._done = False
        for record in partition.read():
            self._output_queue.put(record)
        self._done = True

    def is_done(self) -> bool:
        return self._output_queue.qsize() == 0 and self._done

    def has_record_ready(self) -> bool:
        return self._output_queue.qsize() > 0

    def get_next(self) -> Optional[Record]:
        if self._output_queue.qsize() > 0:
            return self._output_queue.get()
        else:
            return None