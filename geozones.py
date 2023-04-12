import os

import openai
import requests
import tiktoken
from github import Github

# MODEL = "gpt-4-0314"
MODEL = "gpt-3.5-turbo-0301"


# Replace with the name of the repository and the access token
repository_name = "pokt-network/pocket"
access_token = os.getenv("GITHUB_ACCESS_TOKEN")


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            num_tokens += (
                4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            )
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not presently implemented for model {model}.
  See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )


# Define a recursive function to loop through the contents of a directory
def process_directory(repo, path, extensions):
    contents = repo.get_contents(path)
    for content in contents:
        if content.type == "dir":
            yield from process_directory(repo, content.path, extensions)
        elif content.type == "file":
            if any(content.name.endswith(ext) for ext in extensions):
                # print(content.path)
                yield content.path


def filter_files(files, keywords):
    for file in files:
        if any(keyword in file for keyword in keywords):
            yield file


def gpt_messages(code: str):
    return [
        {"role": "system", "content": "You are a senior software engineer."},
        {
            "role": "user",
            "content": "I will provide you with some code you need to refactor.",
        },
        {
            "role": "assistant",
            "content": "Where is the code?",
        },
        {"role": "user", "content": code},
        {
            "role": "assistant",
            "content": "What should I do with it?",
        },
        {
            "role": "user",
            "content": "Provide a git diff that introduces a 'geoZones' string slice with similar business logic to all instances of 'relay', 'relay_chain', 'relaychain', 'relay-chain', or 'relay chain'.",
        },
    ]


file_extensions = [".go"]
keywords = ["chain", "relay_chain", "relaychain", "relay-chain", "relay chain"]


def main():
    g = Github(access_token)
    repo = g.get_repo(repository_name)
    openai.api_key = os.getenv("OPENAI_API_KEY")
    # files = process_directory(repo, "", file_extensions)
    # print(files)
    filtered_files = filter_files(files, keywords)

    for file in filtered_files:
        file_contents = repo.get_contents(file)
        file_content_str = file_contents.decoded_content.decode("utf-8")
        msgs = gpt_messages(file_content_str)
        print("Before")
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=msgs,
        )
        print("After")

        # num_tokens = num_tokens_from_messages(msgs)  # gpt4 is not supported yet
        # print("Num tokens", num_tokens)

        print(response)

        break


files = [
    "app/app.go",
    "app/client/cli/account.go",
    "app/client/cli/actor.go",
    "app/client/cli/cmd.go",
    "app/client/cli/consensus.go",
    "app/client/cli/debug.go",
    "app/client/cli/docgen/main.go",
    "app/client/cli/gov.go",
    "app/client/cli/keys.go",
    "app/client/cli/query.go",
    "app/client/cli/system.go",
    "app/client/cli/utils.go",
    "app/client/cli/utils_test.go",
    "app/client/debug.go",
    "app/client/keybase/debug/keystore.go",
    "app/client/keybase/hashicorp/vault.go",
    "app/client/keybase/hashicorp/vault_test.go",
    "app/client/keybase/keybase.go",
    "app/client/keybase/keybase_test.go",
    "app/client/keybase/keystore.go",
    "app/client/main.go",
    "app/pocket/main.go",
    "build/config/main.go",
    "build/debug.go",
    "build/debug_keybase/main.go",
    "build/dummy.go",
    "build/linters/tests.go",
    "build/localnet/cluster-manager/main.go",
    "build/localnet/cluster-manager/utils.go",
    "consensus/block.go",
    "consensus/debugging.go",
    "consensus/e2e_tests/hotstuff_test.go",
    "consensus/e2e_tests/pacemaker_test.go",
    "consensus/e2e_tests/state_sync_test.go",
    "consensus/e2e_tests/utils_test.go",
    "consensus/events.go",
    "consensus/fsm_handler.go",
    "consensus/helpers.go",
    "consensus/hotstuff_handler.go",
    "consensus/hotstuff_leader.go",
    "consensus/hotstuff_mempool.go",
    "consensus/hotstuff_mempool_test.go",
    "consensus/hotstuff_replica.go",
    "consensus/leader_election/module.go",
    "consensus/leader_election/sortition/sortition.go",
    "consensus/leader_election/sortition/sortition_test.go",
    "consensus/leader_election/vrf/errors.go",
    "consensus/leader_election/vrf/vrf.go",
    "consensus/leader_election/vrf/vrf_test.go",
    "consensus/messages.go",
    "consensus/module.go",
    "consensus/module_consensus_debugging.go",
    "consensus/module_consensus_pacemaker.go",
    "consensus/module_consensus_state_sync.go",
    "consensus/pacemaker/debug.go",
    "consensus/pacemaker/module.go",
    "consensus/state_sync/helpers.go",
    "consensus/state_sync/interfaces.go",
    "consensus/state_sync/module.go",
    "consensus/state_sync/server.go",
    "consensus/state_sync_handler.go",
    "consensus/telemetry/metrics.go",
    "consensus/types/actor_mapper.go",
    "consensus/types/actor_mapper_test.go",
    "consensus/types/messages.go",
    "consensus/types/types.go",
    "e2e/tests/steps_init_test.go",
    "e2e/tests/validator.go",
    "libp2p/module.go",
    "libp2p/network/network.go",
    "libp2p/network/network_test.go",
    "libp2p/network/peer_conversion.go",
    "libp2p/network/url_conversion.go",
    "libp2p/network/url_conversion_test.go",
    "libp2p/network/utils_test.go",
    "libp2p/protocol/protocol.go",
    "libp2p/transport/transport.go",
    "libp2p/types/mocks/mocks.go",
    "logger/module.go",
    "p2p/bootstrap.go",
    "p2p/event_handler.go",
    "p2p/module.go",
    "p2p/module_raintree_test.go",
    "p2p/module_test.go",
    "p2p/peer_test.go",
    "p2p/providers/current_height_provider/current_height_provider.go",
    "p2p/providers/current_height_provider/rpc/provider.go",
    "p2p/providers/peerstore_provider/errors.go",
    "p2p/providers/peerstore_provider/peerstore_provider.go",
    "p2p/providers/peerstore_provider/persistence/provider.go",
    "p2p/providers/peerstore_provider/rpc/provider.go",
    "p2p/providers/providers.go",
    "p2p/raintree/network.go",
    "p2p/raintree/network_test.go",
    "p2p/raintree/nonce_deduper.go",
    "p2p/raintree/nonce_deduper_test.go",
    "p2p/raintree/peers_manager.go",
    "p2p/raintree/peers_manager_test.go",
    "p2p/raintree/peerstore_utils.go",
    "p2p/raintree/target.go",
    "p2p/raintree/utils_test.go",
    "p2p/stdnetwork/network.go",
    "p2p/transport/transport.go",
    "p2p/transport/transport_test.go",
    "p2p/types/errors.go",
    "p2p/types/mocks/mocks.go",
    "p2p/types/network.go",
    "p2p/types/network_peer.go",
    "p2p/types/transport.go",
    "p2p/utils_test.go",
    "persistence/account.go",
    "persistence/account_shared_sql.go",
    "persistence/actor.go",
    "persistence/actor_shared_sql.go",
    "persistence/application.go",
    "persistence/block.go",
    "persistence/context.go",
    "persistence/db.go",
    "persistence/debug.go",
    "persistence/fisherman.go",
    "persistence/genesis.go",
    "persistence/gov.go",
    "persistence/indexer/indexer.go",
    "persistence/indexer/indexer_test.go",
    "persistence/kvstore/kvstore.go",
    "persistence/module.go",
    "persistence/servicer.go",
    "persistence/state.go",
    "persistence/test/account_test.go",
    "persistence/test/actor_test.go",
    "persistence/test/application_test.go",
    "persistence/test/benchmark_state_test.go",
    "persistence/test/block_test.go",
    "persistence/test/fisherman_test.go",
    "persistence/test/generic_test.go",
    "persistence/test/gov_test.go",
    "persistence/test/module_test.go",
    "persistence/test/servicer_test.go",
    "persistence/test/setup_test.go",
    "persistence/test/state_test.go",
    "persistence/test/validator_test.go",
    "persistence/types/account.go",
    "persistence/types/account_shared_sql.go",
    "persistence/types/actor_shared_sql.go",
    "persistence/types/application.go",
    "persistence/types/base_account.go",
    "persistence/types/base_actor.go",
    "persistence/types/block.go",
    "persistence/types/fisherman.go",
    "persistence/types/gov.go",
    "persistence/types/gov_test.go",
    "persistence/types/mocks/mocks.go",
    "persistence/types/pool.go",
    "persistence/types/protocol_account.go",
    "persistence/types/protocol_actor.go",
    "persistence/types/servicer.go",
    "persistence/types/validator.go",
    "persistence/validator.go",
    "rpc/handlers.go",
    "rpc/module.go",
    "rpc/noop_module.go",
    "rpc/pprof.go",
    "rpc/rpc.go",
    "rpc/server.go",
    "rpc/types/types.go",
    "runtime/bus.go",
    "runtime/configs/config.go",
    "runtime/configs/types/keybase_ext.go",
    "runtime/defaults/defaults.go",
    "runtime/environment.go",
    "runtime/errors.go",
    "runtime/genesis.go",
    "runtime/manager.go",
    "runtime/manager_test.go",
    "runtime/modules_registry.go",
    "runtime/test_artifacts/defaults.go",
    "runtime/test_artifacts/generator.go",
    "runtime/test_artifacts/genesis.go",
    "runtime/test_artifacts/gov.go",
    "runtime/test_artifacts/keygen/keygen.go",
    "runtime/test_artifacts/util.go",
    "shared/codec/codec.go",
    "shared/codec/codec_test.go",
    "shared/core/types/actor.go",
    "shared/core/types/fsm_events.go",
    "shared/core/types/fsm_states.go",
    "shared/core/types/pools.go",
    "shared/core/types/pools_test.go",
    "shared/core/types/signature.go",
    "shared/core/types/transaction.go",
    "shared/core/types/transaction_test.go",
    "shared/crypto/armour.go",
    "shared/crypto/ed25519.go",
    "shared/crypto/error.go",
    "shared/crypto/keypair.go",
    "shared/crypto/keys.go",
    "shared/crypto/libp2p.go",
    "shared/crypto/rand.go",
    "shared/crypto/sha3.go",
    "shared/crypto/slip/slip.go",
    "shared/crypto/slip/slip_test.go",
    "shared/k8s/debug.go",
    "shared/mempool/generic_fifo_set.go",
    "shared/mempool/list/generic_fifo_list.go",
    "shared/mempool/tx_mempool.go",
    "shared/messaging/envelope.go",
    "shared/messaging/envelope_test.go",
    "shared/messaging/events.go",
    "shared/messaging/messages.go",
    "shared/messaging/messages_test.go",
    "shared/modules/base_modules/integratable_module.go",
    "shared/modules/base_modules/interruptable_module.go",
    "shared/modules/bus_module.go",
    "shared/modules/consensus_module.go",
    "shared/modules/factory.go",
    "shared/modules/logger_module.go",
    "shared/modules/mocks/mocks.go",
    "shared/modules/module.go",
    "shared/modules/modules_registry_module.go",
    "shared/modules/p2p_module.go",
    "shared/modules/persistence_module.go",
    "shared/modules/rpc_module.go",
    "shared/modules/runtime_module.go",
    "shared/modules/state_machine_module.go",
    "shared/modules/telemetry_module.go",
    "shared/modules/tx_result.go",
    "shared/modules/utility_module.go",
    "shared/node.go",
    "shared/p2p/peer.go",
    "shared/p2p/peer_manager.go",
    "shared/p2p/peers_view.go",
    "shared/p2p/peers_view_test.go",
    "shared/p2p/peerstore.go",
    "shared/utils/file_utils.go",
    "shared/utils/gov_utils.go",
    "shared/utils/num_utils.go",
    "shared/utils/num_utils_test.go",
    "state_machine/fsm.go",
    "state_machine/module.go",
    "state_machine/visualizer/main.go",
    "telemetry/errors.go",
    "telemetry/metrics_p2p.go",
    "telemetry/module.go",
    "telemetry/noop_module.go",
    "telemetry/prometheus_module.go",
    "utility/module.go",
    "utility/service/service.go",
    "utility/session.go",
    "utility/transaction.go",
    "utility/types/constants.go",
    "utility/types/error.go",
    "utility/types/gov.go",
    "utility/types/message.go",
    "utility/types/message_staking.go",
    "utility/types/message_test.go",
    "utility/types/relay_chain.go",
    "utility/types/relay_chain_test.go",
    "utility/types/tx_fifo_mempool.go",
    "utility/types/tx_fifo_mempool_test.go",
    "utility/types/tx_result.go",
    "utility/unit_of_work/account.go",
    "utility/unit_of_work/account_test.go",
    "utility/unit_of_work/actor.go",
    "utility/unit_of_work/actor_test.go",
    "utility/unit_of_work/application.go",
    "utility/unit_of_work/application_test.go",
    "utility/unit_of_work/block.go",
    "utility/unit_of_work/block_test.go",
    "utility/unit_of_work/gov.go",
    "utility/unit_of_work/gov_test.go",
    "utility/unit_of_work/message_test.go",
    "utility/unit_of_work/module.go",
    "utility/unit_of_work/module_test.go",
    "utility/unit_of_work/transaction.go",
    "utility/unit_of_work/transaction_test.go",
    "utility/unit_of_work/tx_message_handler.go",
    "utility/unit_of_work/uow_leader.go",
    "utility/unit_of_work/uow_replica.go",
    "utility/unit_of_work/validator.go",
    "utility/uow.go",
    "utility/utility_message_handler.go",
]


if __name__ == "__main__":
    main()
