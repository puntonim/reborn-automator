from dataclasses import dataclass


class LambdaContextFactory:
    @staticmethod
    def make():
        @dataclass
        class LambdaContext:
            function_name: str = __name__
            memory_limit_in_mb: int = 128
            invoked_function_arn: str = (
                "arn:aws:lambda:eu-west-1:809313241:function:" + __name__
            )
            aws_request_id: str = "52fdfc07-2182-154f-163f-5f0f9a621d72"

        return LambdaContext()
