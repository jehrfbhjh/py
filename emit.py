def emit(self, record):
    self.acquire()

    try:
        if not self.connection or self.connection.is_closed or not self.channel or self.channel.is_closed:
            self.open_connection()

        if self.routing_key_formatter:
            routing_key = self.routing_key_formatter(record)
        else:
            routing_key = self.routing_key_format.format(
                name=record.name,
                level=record.levelname
            )

        if hasattr(record, 'request'):
            no_exc_record = copy(record)
            del no_exc_record.exc_info
            del no_exc_record.exc_text
            del no_exc_record.request

            if record.exc_info:
                exc_info = record.exc_info
            else:
                exc_info = (None, record.getMessage(), None)

            # Get a text representation of the exception.
            if ExceptionReporter:
                reporter = ExceptionReporter(record.request, is_email=False, *exc_info)
                no_exc_record.traceback = reporter.get_traceback_text()

            formatted = self.format(no_exc_record)
        else:
            formatted = self.format(record)

        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=routing_key,
            body=formatted,
            properties=pika.BasicProperties(
                delivery_mode=2,
                headers=self.message_headers
            )
        )

    except Exception:
        self.channel, self.connection = None, None
        self.handleError(record)
    finally:
        if self.close_after_emit:
            self.close_connection()

        self.release()