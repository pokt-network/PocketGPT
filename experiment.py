import json
import os

import openai
from file_generator import get_code
from github_issue import get_github_issue_description
from messages import get_messages, get_messages_test
from token_counter import num_tokens_from_messages

openai.api_key = os.getenv("OPENAI_API_KEY")

# MODEL = "gpt-4-32k-0314"
MODEL = "gpt-4-0314"
MAX_TOKENS = ""

URL = "https://github.com/pokt-network/pocket/issues/569"

directory = "/Users/olshansky/workspace/pocket/pocket"

# Set the name of the file to write the concatenated code to
output_file = "/Users/olshansky/workspace/pocket/code.txt"

# Set the list of regular expressions to use for exclusion
exclude_patterns = [
    # exclude files without extensions
    "^[^.]*$",
    # Don't include dependencies
    ".*vendor.*",
    "go.mod",
    "go.sum",
    # Don't include test files
    ".*_test.go",
    # Don't include changelogs
    "CHANGELOG*",
    # Don't include auto generated docs
    "client_.*.md",
    # Don't include meeting nodes
    "devlog.*.md",
    "demos",
    # Don't include supporting files
    ".*.json",
    ".*.yaml",
    ".*.sql",
    # ".*.sh", # Why doesn't this work?
    ".*.mk",
    # Don't include images
    ".*.gif",
    ".*.jpg",
    ".*.png",
    # Don't include generated proto files
    ".*.pb.go",
    ".*_mock.go",
    # Trying to reduce num of tokens - 1
    "Docker.*",
    "shared/k8s/.*",
    # Trying to reduce num of tokens - 2
    "/consensus/.*",
    "/persistence/.*",
    "/libp2p/.*",
    "/p2p/.*",
    # Trying to reduce num of tokens - 3
    "shared/crypto/.*",
    "runtime/configs/*",
    # Trying to reduce num of tokens - 4
]

exclude_files = [
    "/Users/olshansky/workspace/pocket/pocket/runtime/genesis/proto/genesis.proto",
    "/Users/olshansky/workspace/pocket/pocket/shared/node.go",
    # "/Users/olshansky/workspace/pocket/pocket/shared/core/types/pools.go",
    # "/Users/olshansky/workspace/pocket/pocket/shared/core/types/fsm_events.go",
    "/Users/olshansky/workspace/pocket/pocket/shared/core/types/transaction.go",
    # "/Users/olshansky/workspace/pocket/pocket/shared/core/types/fsm_states.go",
    "/Users/olshansky/workspace/pocket/pocket/shared/core/types/signature.go",
    # "/Users/olshansky/workspace/pocket/pocket/shared/core/types/actor.go",
    "/Users/olshansky/workspace/pocket/pocket/shared/core/types/proto/transaction.proto",
    # "/Users/olshansky/workspace/pocket/pocket/shared/core/types/proto/account.proto",
    # "/Users/olshansky/workspace/pocket/pocket/shared/core/types/proto/actor.proto",
    "/Users/olshansky/workspace/pocket/pocket/shared/core/types/proto/block.proto",
    "/Users/olshansky/workspace/pocket/pocket/shared/core/types/proto/param.proto",
    # "/Users/olshansky/workspace/pocket/pocket/shared/core/types/proto/pools.proto",
    "/Users/olshansky/workspace/pocket/pocket/shared/codec/codec.go",
    "/Users/olshansky/workspace/pocket/pocket/shared/codec/proto/codec_test.proto",
    "/Users/olshansky/workspace/pocket/pocket/shared/utils/file_utils.go",
    "/Users/olshansky/workspace/pocket/pocket/shared/utils/num_utils.go",
    "/Users/olshansky/workspace/pocket/pocket/shared/mempool/generic_fifo_set.go",
    "/Users/olshansky/workspace/pocket/pocket/shared/mempool/tx_mempool.go",
    "/Users/olshansky/workspace/pocket/pocket/shared/mempool/list/generic_fifo_list.go",
    # "/Users/olshansky/workspace/pocket/pocket/shared/modules/utility_module.go",
    "/Users/olshansky/workspace/pocket/pocket/shared/modules/rpc_module.go",
    "/Users/olshansky/workspace/pocket/pocket/shared/modules/state_machine_module.go",
    "/Users/olshansky/workspace/pocket/pocket/shared/modules/tx_result.go",
    "/Users/olshansky/workspace/pocket/pocket/shared/modules/telemetry_module.go",
    "/Users/olshansky/workspace/pocket/pocket/shared/modules/p2p_module.go",
    "/Users/olshansky/workspace/pocket/pocket/shared/modules/consensus_module.go",
    # "/Users/olshansky/workspace/pocket/pocket/shared/modules/persistence_module.go",
    "/Users/olshansky/workspace/pocket/pocket/shared/modules/bus_module.go",
    "/Users/olshansky/workspace/pocket/pocket/shared/modules/runtime_module.go",
    "/Users/olshansky/workspace/pocket/pocket/shared/modules/logger_module.go",
    "/Users/olshansky/workspace/pocket/pocket/shared/modules/modules_registry_module.go",
    "/Users/olshansky/workspace/pocket/pocket/shared/modules/module.go",
    "/Users/olshansky/workspace/pocket/pocket/shared/modules/mocks/mocks.go",
    "/Users/olshansky/workspace/pocket/pocket/shared/modules/types/proto/unstaking_actor.proto",
    "/Users/olshansky/workspace/pocket/pocket/shared/modules/base_modules/interruptable_module.go",
    "/Users/olshansky/workspace/pocket/pocket/shared/modules/base_modules/integratable_module.go",
    "/Users/olshansky/workspace/pocket/pocket/shared/messaging/events.go",
    "/Users/olshansky/workspace/pocket/pocket/shared/messaging/messages.go",
    "/Users/olshansky/workspace/pocket/pocket/shared/messaging/envelope.go",
    "/Users/olshansky/workspace/pocket/pocket/shared/messaging/proto/events.proto",
    "/Users/olshansky/workspace/pocket/pocket/shared/messaging/proto/debug_message.proto",
    "/Users/olshansky/workspace/pocket/pocket/shared/messaging/proto/pocket_envelope.proto",
    "/Users/olshansky/workspace/pocket/pocket/utility/validator.go",
    # "/Users/olshansky/workspace/pocket/pocket/utility/session.go",
    "/Users/olshansky/workspace/pocket/pocket/utility/transaction.go",
    "/Users/olshansky/workspace/pocket/pocket/utility/utility_message_handler.go",
    "/Users/olshansky/workspace/pocket/pocket/utility/context.go",
    "/Users/olshansky/workspace/pocket/pocket/utility/application.go",
    "/Users/olshansky/workspace/pocket/pocket/utility/tx_message_handler.go",
    "/Users/olshansky/workspace/pocket/pocket/utility/account.go",
    "/Users/olshansky/workspace/pocket/pocket/utility/gov.go",
    "/Users/olshansky/workspace/pocket/pocket/utility/actor.go",
    "/Users/olshansky/workspace/pocket/pocket/utility/block.go",
    "/Users/olshansky/workspace/pocket/pocket/utility/module.go",
    "/Users/olshansky/workspace/pocket/pocket/utility/types/message_staking.go",
    "/Users/olshansky/workspace/pocket/pocket/utility/types/error.go",
    "/Users/olshansky/workspace/pocket/pocket/utility/types/tx_fifo_mempool.go",
    "/Users/olshansky/workspace/pocket/pocket/utility/types/relay_chain.go",
    "/Users/olshansky/workspace/pocket/pocket/utility/types/tx_result.go",
    "/Users/olshansky/workspace/pocket/pocket/utility/types/message.go",
    "/Users/olshansky/workspace/pocket/pocket/utility/types/constants.go",
    "/Users/olshansky/workspace/pocket/pocket/utility/types/gov.go",
    "/Users/olshansky/workspace/pocket/pocket/utility/types/proto/tx_result.proto",
    "/Users/olshansky/workspace/pocket/pocket/utility/types/proto/message.proto",
    "/Users/olshansky/workspace/pocket/pocket/utility/types/proto/utility_messages.proto",
    "/Users/olshansky/workspace/pocket/pocket/utility/service/service.go",
]

# include_list = [".*.go", ".*.md"]
include_list = ["utility/.*.go", "shared/.*.go", ".*.proto"]  # , ".*.md", ]


if __name__ == "__main__":
    description = get_github_issue_description(URL)
    code = get_code(
        directory, output_file, include_list, exclude_patterns, exclude_files
    )
    messages = get_messages(code, description)
    # messages = get_messages_test()
    num_tokens = num_tokens_from_messages(messages)  # gpt4 is not supported yet
    print(
        num_tokens,
    )
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
    )

    # Serializing json
    json_object = json.dumps(response, indent=4)

    # Writing to response.json
    with open("response_test.json", "w") as outfile:
        outfile.write(json_object)
