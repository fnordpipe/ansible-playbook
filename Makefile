export PLAYBOOK_VAULT_DIR?=../vault

check:
	# invoke dry-run

	ansible-playbook -i ${PLAYBOOK_VAULT_DIR}/production.ini ./site.yml --check

lxd:
	# run only lcd's

	ansible-playbook -i ${PLAYBOOK_VAULT_DIR}/production.ini ./site.yml --limit lxd

dom0:
	# invoke real-run

	ansible-playbook -i ${PLAYBOOK_VAULT_DIR}/production.ini ./site.yml --limit dom0
