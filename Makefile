export PLAYBOOK_VAULT_DIR?=../vault
export PLAYBOOK_INVENTORY_DIR?=../inventory

check:
	# invoke dry-run

	ansible-playbook -i ${PLAYBOOK_INVENTORY_DIR}/production.ini ./site.yml --check

run:
	# invoke real-run

	ansible-playbook -i ${PLAYBOOK_INVENTORY_DIR}/production.ini ./site.yml
